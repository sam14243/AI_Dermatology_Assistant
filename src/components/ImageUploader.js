import React, { useState } from 'react';
import { Loading } from 'react-simple-chatbot';
import PropTypes from 'prop-types';

const handleImageSubmit = async (img) => {
    fetch('https://e949-115-244-132-22.ngrok-free.app/image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': '0'
        },
        body: JSON.stringify({ 'userid':'abhi', 'image': img })
    })
    .then(response => {
        if (response.ok) {
            console.log("image sent");
            console.log("image response:",response);
        } else {
            console.error('Failed to upload image');
        }
    });
};

const ImageUploader = ({ triggerNextStep }) => {
    const [loading, setLoading] = useState(false);
    const [imageUrl, setImageUrl] = useState(null);
  
    const handleFileUpload = (event) => {
      const file = event.target.files[0];
  
      if (file) {
        setLoading(true);
  
        const reader = new FileReader();
        reader.onloadend = () => {
            setLoading(false);
            setImageUrl(reader.result);
            handleImageSubmit(reader.result);
            triggerNextStep();
        };
        reader.readAsDataURL(file);
      }
    };
  
    return (
      <div className="imageUploader">
        {loading ? (
          <Loading />
        ) : imageUrl ? (
          <div>
            <img src={imageUrl} alt="Uploaded Image" style={{ maxWidth: '100%', maxHeight: '200px' }} />
            <p>Preview of the uploaded image</p>
          </div>
        ) : (
          <div style={{ textAlign: 'center', marginTop: 20 }}>
            <input style={{fontSize:"16px"}}type="file" accept="image/*" onChange={handleFileUpload} />
          </div>
        )}
      </div>
    );
};

ImageUploader.propTypes = {
  triggerNextStep: PropTypes.func,
};

ImageUploader.defaultProps = {
  triggerNextStep: undefined,
};

export default ImageUploader;

// import React, { useState } from 'react';

// function ImageUploader({ triggerNextStep }) {
//     const [image, setImage] = useState(null);

//     const handleImageChange = (e) => {
//         const file = e.target.files[0];
//         if (file) {
//             const reader = new FileReader();
//             reader.onload = (event) => {
//                 setImage(event.target.result);
//             };
//             reader.readAsDataURL(file);
//         }
//     };

//     const handleSubmit = (e) => {
//         e.preventDefault();
        
//         if (image) {
//             fetch('https://868b-115-244-132-22.ngrok-free.app/image', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'ngrok-skip-browser-warning': '0'
//                 },
//                 body: JSON.stringify({ 'userid':'abhi', 'image': image })

//             })
//             .then(response => {
//                 if (response.ok) {
//                     console.log('Form submitted successfully:', response);
//                     triggerNextStep();
//                 } else {
//                     console.error('Failed to submit form');
//                 }
//             })
//             .catch(error => {
//                 console.error('Error submitting form:', error);
//             });
//         }
        
//     };

//     return (
//         <div>
//             <form onSubmit={handleSubmit}>
//                 <input type="file" accept="image/*" onChange={handleImageChange} />
//                 {image && <img src={image} alt="Selected" style={{ maxWidth: '300px' }} />}
//                 <button type="submit">Submit</button>
//             </form>
//         </div>
//     );
// }

// export default ImageUploader;

