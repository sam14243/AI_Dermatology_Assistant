import React, { useEffect } from 'react';

const Result = ({ location, time, appearance, symptoms  }) => {
  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log({location});
        console.log(time);
        console.log(symptoms);
        console.log(appearance);
        const response = await fetch('https://8fee-60-243-70-8.ngrok-free.app/symptoms', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': '0'
          },
          body: JSON.stringify({'userid':'abhi', 'location': location, 'time':time, 'appearance':appearance, 'symptoms':symptoms })
        });

        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }

        // If you need to do something with the response from the backend
        const data = await response.json();
        console.log('Response from backend:', data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [location, time, appearance, symptoms]);

  return (
    <div>
      <h3>DONE!!</h3>
    </div>
  );
};

export default Result;
