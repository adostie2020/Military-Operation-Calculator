import React, { useState } from 'react';
import './main.css'; // Import the CSS file


const Main = () => {
  const [inputs, setInputs] = useState({ aircraftType: [] });
  const [missingFields, setMissingFields] = useState(null);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    if (type === 'checkbox') {
      if (name === 'aircraftType') {
        setInputs((prevInputs) => {
          const updatedAircraftType = checked
            ? [...prevInputs.aircraftType, value]
            : prevInputs.aircraftType.filter((type) => type !== value);

          return {
            ...prevInputs,
            [name]: updatedAircraftType,
          };
        });
      } else {
        setInputs((prevInputs) => ({
          ...prevInputs,
          [name]: checked,
        }));
      }
    } else {
      setInputs((prevInputs) => ({
        ...prevInputs,
        [name]: value,
      }));
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const requiredFields = ['departureCity', 'departureDate', 'arrivalCity', 'arrivalDate', 'numOfSupporters', 'flyOption', 'aircraftType', 'lodging'];
    const inputMissingFields = requiredFields.filter(field => !inputs[field]);
    console.log(inputMissingFields);
    console.log(inputMissingFields.length);
    console.log(inputs.aircraftType);
    setMissingFields(false);
    if (inputMissingFields.length > 0 || inputs.aircraftType.length === 0) {
      setMissingFields(true);
    }
    console.log("Missing fields is " + missingFields);
  };


  function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdown-content");
    dropdownContent.style.display = dropdownContent.style.display === "none" ? "block" : "none";
  }


  return (
    <div className='Form'>
      <h1 className='Title'>PACAF Calculator</h1>
      <form onSubmit={handleSubmit}>
        <label className='departureCity'>
          From:<p className='required-star'>*</p>
          <input type="text" name="departureCity" value={inputs.departureCity || ''} onChange={handleChange} />
        </label>
        <label className='departureDate'>
          Select a Date:<p className='required-star'>*</p>
          <input type="date" name="departureDate" value={inputs.departureDate} onChange={handleChange} />
        </label>
        <br />
        <label className='arrivalCity'>
          To:<p className='required-star'>*</p>
          <input type="text" name="arrivalCity" value={inputs.arrivalCity || ''} onChange={handleChange} />
        </label>
        <label className='arrivalDate'>
          Select a Date:<p className='required-star'>*</p>
          <input type="date" name="arrivalDate" value={inputs.arrivalDate} onChange={handleChange} />
        </label>
        <br />
        <label className='supporters'>
          Number of Supporters:<p className='required-star'>*</p>
          <input type="number" name="numOfSupporters" value={inputs.numOfSupporters || ''} onChange={handleChange} />
        </label>
        <br />
        <label className='airfare'>
          Airfare Type:<p className='required-star'>*</p>
          <select value={inputs.flyOption} name="flyOption" onChange={handleChange}>
            <option value="">-- Select --</option>
            <option value="militaryAir">Military Air</option>
            <option value="commercialAir">Commercial Air</option>
          </select>
        </label>

        <label className='aircraftType'>
          Aircraft Type:<p className='required-star'>*</p>
          <div className="dropdown">
            <button className="dropdown-toggle" onClick={toggleDropdown}>Select Aircraft Type</button>
            <div id="dropdown-content" className="dropdown-content">
              <label>
                <input
                  type="checkbox"
                  value="militaryAir"
                  name="aircraftType"
                  onChange={handleChange}
                  checked={inputs.aircraftType && inputs.aircraftType.includes("militaryAir")}
                />
                Military Air
                {inputs.aircraftType && inputs.aircraftType.includes("militaryAir") && (
                  <input
                    type="number"
                    name="militaryAirQuantity"
                    value={inputs.militaryAirQuantity || ''}
                    onChange={handleChange}
                  />
                )}
              </label>
              <label>
                <input
                  type="checkbox"
                  value="commercialAir"
                  name="aircraftType"
                  onChange={handleChange}
                  checked={inputs.aircraftType && inputs.aircraftType.includes("commercialAir")}
                />
                Commercial Air
                {inputs.aircraftType && inputs.aircraftType.includes("commercialAir") && (
                  <input
                    type="number"
                    name="commercialAirQuantity"
                    value={inputs.commercialAirQuantity || ''}
                    onChange={handleChange}
                  />
                )}
              </label>
            </div>
          </div>
        </label>

        <br />
        <label className='lodging'>
          Lodging:<p className='required-star'>*</p>
          <select value={inputs.lodging} name="lodging" onChange={handleChange}>
            <option value="">-- Select --</option>
            <option value="govLodging">Government Lodging</option>
            <option value="commLodging">Commercial Hotel Lodging</option>
            <option value="fieldConditions">Field Conditions</option>
          </select>
        </label>

        <label>
          Meal Provided:
          <input type="checkbox" checked={inputs.mealProvided} onChange={handleChange} />
        </label>



        {missingFields && <p className='missingFields'>Please Fill out all required fields</p>}
        <br />
        <button type="calculate">Calculate</button>
      </form>
    </div>
  );
};

export default Main;