import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useState } from 'react';

export const handleTextSubmit = (text) => {
    return axios.post('https://e949-115-244-132-22.ngrok-free.app/chat/query', {
        userid: 'abhi',
        query: text
    }, {
        headers: {
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': '0'
        }
    })
    .then(response => {
        console.log("Text received");
        return response.data;
    });
};

const ChatUploader = ({ triggerNextStep, previousStep }) => {
    console.log(previousStep.message);
    const [data, setData] = useState(null);
    if (!data) {
        handleTextSubmit(previousStep.message)
        .then(result => {
            setData(result);
            triggerNextStep();
        });
    };
    console.log("data: ", data);
    return <div>{data}</div>;
};

ChatUploader.propTypes = {
    triggerNextStep: PropTypes.func,
};

ChatUploader.defaultProps = {
    triggerNextStep: undefined,
};

export default ChatUploader;