import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

def run():
    st.title("🧠 Teachable Machine - Streamlit Version")
    st.write("Upload multiple images per class and train your own model!")

    # Step 1: Number of classes
    num_classes = st.number_input("How many classes?", 2, 10, 2)

    data = {}
    for i in range(num_classes):
        st.subheader(f"Class {i+1} Images")
        files = st.file_uploader(
            f"Upload images for Class {i+1}", 
            accept_multiple_files=True, 
            type=['jpg','png','jpeg'],
            key=f"c{i}"
        )
        data[i] = files

    # Step 2: Load MobileNetV2
    @st.cache_resource
    def load_feature_extractor():
        base = tf.keras.applications.MobileNetV2(
            input_shape=(224,224,3),
            include_top=False,
            weights="imagenet",
            pooling="avg"
        )
        return base

    feature_extractor = load_feature_extractor()

    # Step 3: Preprocess
    def preprocess(img):
        img = img.resize((224,224))
        img = np.array(img) / 255.0
        return np.expand_dims(img, axis=0)

    # Step 4: Train Model
    if st.button("Train Model"):
        X = []
        Y = []

        st.write("Processing images...")

        for class_id, files in data.items():
            if files:
                for file in files:
                    img = Image.open(file).convert("RGB")
                    tensor = preprocess(img)

                    features = feature_extractor(tensor)
                    X.append(features.numpy()[0])
                    Y.append(class_id)

        X = np.array(X)
        Y = tf.keras.utils.to_categorical(Y, num_classes)

        st.write("Training... Please wait.")

        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(1280,)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(num_classes, activation="softmax")
        ])

        model.compile(
            optimizer=tf.keras.optimizers.Adam(1e-4),
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )

        model.fit(X, Y, epochs=10, batch_size=8, verbose=0)

        st.success("🎉 Training Completed!")
        st.session_state["model"] = model

    # Step 5: Prediction
    st.header("🔍 Predict New Image")

    predict_file = st.file_uploader("Upload image to classify", type=['jpg','png','jpeg'])

    if predict_file and "model" in st.session_state:
        image = Image.open(predict_file).convert("RGB")
        st.image(image, width=250)

        tensor = preprocess(image)
        features = feature_extractor(tensor)
        pred = st.session_state["model"].predict(features)[0]

        class_id = np.argmax(pred)

        st.subheader(f"🟢 Prediction: Class {class_id+1}")
        st.write("Probabilities:", pred)

    else:
        st.info("Upload image and train model first.")
