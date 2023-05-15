import React, { useState } from 'react';
import './main.css'; // Import the CSS file


const Main = () => {
    const [inputs, setInputs] = useState({});

  const handleChange = (event) => {
    const { name, value } = event.target;
    setInputs((prevState) => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Perform any desired action with the form inputs
    console.log(inputs);
  };

  return (
    <div className='Form'>
      <h1 className='Title'>PACAF Calculator</h1>
      <form onSubmit={handleSubmit}>
        <label className='departureCity'>
          From:
          <input type="text" name="departureCity" value={inputs.departureCity || ''} onChange={handleChange} />
        </label>
        <label className='departureDate'>
          Select a Date:
          <input type="date" value={inputs.departureDate} onChange={handleChange} />
        </label>
        <br />
        <label className='arrivalCity'>
          To:
          <input type="text" name="arrivalCity" value={inputs.arrivalCity || ''} onChange={handleChange} />
        </label>
        <label className='arrivalDate'>
          Select a Date:
          <input type="date" value={inputs.arrivalDate} onChange={handleChange} />
        </label>
        <br />
        <label className='supporters'>
          Number of Supporters:
          <input type="number" name="numOfSupporters" value={inputs.numOfSupporters || ''} onChange={handleChange} />
        </label>
        <label className='airfare'>
          Airfare Type:
          <select value={inputs.flyOption} onChange={handleChange}>
            <option value="">-- Select --</option>
            <option value="option1">Military Air</option>
            <option value="option2">Commercial Air</option>
          </select>
        </label>
        <label className='numOfAircraft'>
          Number of Aircraft:
          <input type="number" name="numOfAircraft" value={inputs.numOfAircraft || ''} onChange={handleChange} />
        </label>
        <br />
        <label className='lodging'>
          Lodging:
          <select value={inputs.lodging} onChange={handleChange}>
            <option value="">-- Select --</option>
            <option value="option1">Government Lodging</option>
            <option value="option1">Commercial Hotel Lodging</option>
            <option value="option2">Field Conditions</option>
          </select>
        </label>

        <label>
          Meal Provided:
          <input type="checkbox" checked={inputs.mealProvided} onChange={handleChange} />
        </label>
        



        <br />
        {/* Add more input fields as needed */}
        <button type="calculate">Calculate</button>
      </form>
    </div>
  );
};

export default Main;