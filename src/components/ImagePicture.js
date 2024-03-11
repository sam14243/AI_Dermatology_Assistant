import React, { useCallback, useRef, useState } from "react";
import Webcam from 'react-webcam';
import axios from 'axios';


const ImagePicture = ({ triggerNextStep }) => {
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const capture = useCallback(async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImgSrc(imageSrc);
    try {
      const response = await axios.post('https://e949-115-244-132-22.ngrok-free.app/image', {
        userid: 'abhi',
        image: imageSrc, 
        headers: { "Content-Type": "application/json", 'ngrok-skip-browser-warning': '0'},
      });
      console.log('Image uploaded successfully:', response.data);
      triggerNextStep();
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  }, []);

  return (
    <div className="container">
           {imgSrc ? (
            <img src={imgSrc} alt="webcam" />
            ) : (
            <Webcam height={300} width={300} 
            // videoConstraints = { facingMode: { exact: "environment" } }
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg" />
            )}
          <div className="btn-container">
            <button onClick={capture}>Capture photo</button>
          </div>
    </div>
  );
};

export default ImagePicture;