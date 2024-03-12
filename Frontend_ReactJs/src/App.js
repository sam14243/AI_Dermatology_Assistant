import React from 'react';
import ChatBot from 'react-simple-chatbot';
import ImageUploader from './components/ImageUploader';
import ImagePicture from './components/ImagePicture';
import { ThemeProvider } from 'styled-components';
import './App.css';
import axios from 'axios';
import robo from './image/img.png';
import bg from './image/Bgimg.jpg';
import ChatUploader from './components/ChatUploader';

const config = {
  botAvatar: robo
};

const theme = {
  background: '#ECFCFC',
  headerBgColor: '#145B74',
  headerFontSize: '20px',
  botBubbleColor: '#23D3CC',
  headerFontColor: 'white',
  botFontColor: 'white',
  userBubbleColor: '#FF5733',
  userFontColor: 'white',
};
const headers = {
  'Content-Type': 'application/json',
  'ngrok-skip-browser-warning': '0'
};

const App = () => {
  axios.post('https://e949-115-244-132-22.ngrok-free.app/db/del', {
        userid: 'abhi'
    }, {
        headers: {
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': '0'
        }
  });
  const steps = [
    {
      id: '1',
      message: 'Hi, Welcome to AI Dermatology Assistant!',
      trigger: 'preimage'
    },
    {
      id: 'preimage',
      message: 'Would you like to upload or take a picture?',
      trigger: '2',
    },
    {
      id: '2',
      options: [
              { value: 'Upload Image', label: 'Upload Image', trigger: 'upload' },
              { value: 'Take a picture', label: 'Take a picture', trigger: 'image' },
      ],
    },
    {
      id: 'image',
      component: <ImagePicture/>,
      asMessage: true,
      waitAction: true,
      trigger: 'robo',
    },
    {
      id: 'upload',
      component: <ImageUploader/>,
      asMessage: true,
      waitAction: true,
      trigger: 'robo',
    },
    {
      id:'1',
      message:'Checking voice options!',
      trigger: 'userText',
    },
    {
      id: 'userText',
      user: true,
      trigger: 'robo',
    },
    {
      id: 'robo',
      component: <ChatUploader/>,
      asMessage: true,
      waitAction: true,
      trigger: 'userText',
    }
  ]
  return (
    <div className="App" style={{backgroundImage: `url(${bg})`}}>
        {/* <h1>ChatBot</h1> */}
        <ThemeProvider theme={theme}>
          <ChatBot
              steps={steps}
              headerTitle="AI Dermatology Assistant"
              recognitionEnable={true}
              width={"1000px"}
              height={"700px"}
              userDelay="0"
              bubbleStyle={{ fontSize: '14px', textAlign: 'left' }}
              inputStyle={{ fontSize: '14px' }}
              {...config}
          />
        </ThemeProvider>
    </div>
  );
};

export default App;
