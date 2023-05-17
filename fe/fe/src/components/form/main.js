import React, { useState } from 'react';
import './main.css'; // Import the CSS file
import axios from 'axios'

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      aircrafts: [],
      inputs: {},
      missingfields: false,
      formData: []
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleAmount = this.handleAmount.bind(this);
  }

  async componentDidMount() {
    await axios.get('https://hackathon-pacaf--thecosmoking.repl.co/api/get_aircraft')
      .then(response => {
        this.setState({ aircrafts: response.data.aircrafts });
        const newInputs = {};
        for (let i = 0; i < response.data.aircrafts.length; i++) {
          newInputs[response.data.aircrafts[i].type] = false;
        }
        this.setState({ inputs: newInputs })
      })
      .catch(error => {
        console.error(error);
      });
  }


  handleChange(event) {

    const { name, value, type, checked } = event.target;
    if (name === 'aircraftType') {
      const inputsCopy = JSON.parse(JSON.stringify(this.state.inputs));
      inputsCopy[value] = checked;
      this.setState({ inputs: inputsCopy });
      //this.setState(this.state.inputs[value] = checked)
      this.state.inputs[value] = checked;
      console.log("Checking for " + value + " it is " + this.state.inputs[value]);
    }
    else {
      this.setState((prevState) => ({
        inputs: {
          ...prevState.inputs,
          [name]: value,
        },
      }));
    }
  };

  async handleAmount(event) {
    const { name, value, type, checked } = event.target;
    await this.setState((prevState) => ({
      inputs: {
        ...prevState.inputs,
        [name]: parseInt(value),
      },
    }));
    console.log(this.state.inputs);
  }



  handleSubmit(event) {

    event.preventDefault();
    const requiredFields = ['exerciseName', 'departureCity', 'departureDate', 'arrivalCity', 'arrivalDate', 'numOfSupporters', 'flyOption', 'lodging'];

    const hasValue = (obj) => {
      if (typeof obj === 'object' && obj !== null) {
        for (const key in obj) {
          if (!hasValue(obj[key])) {
            return false;
          }
        }
        return true;
      } else {
        return obj !== undefined && obj !== null && obj !== '';
      }
    };
    const inputMissingFields = requiredFields.filter(field => !hasValue(this.state.inputs[field]));
    let noneSelected = true;
    let run = true;
    while (run) {
      if (this.state.inputs["A-10"]) {
        noneSelected = false;
        break;
      }
      else if (this.state.inputs["C-5"]) {
        noneSelected = false;
        break;
      }
      else if (this.state.inputs["C-17"]) {
        noneSelected = false;
        break;
      }
      else if (this.state.inputs["C-130"]) {
        noneSelected = false;
        break;
      }
      else if (this.state.inputs["F-15C"]) {
        noneSelected = false;
        break;
      }
      else if (this.state.inputs["F-22"]) {
        noneSelected = false;
        break;
      }
      else if (this.state.inputs["KC-135"]) {
        noneSelected = false;
        break;
      }
      run = false;
    }
    this.setState({ missingfields: false });
    if (inputMissingFields.length > 0 || noneSelected) {
      this.setState({ missingfields: true }, () => {
      })
    }
  };


  async toggleDropdown() {
    var dropdownContent = document.getElementById("dropdown-content");
    dropdownContent.style.display = dropdownContent.style.display === "none" ? "block" : "none";
  }

  render() {
    return (
      <div className='Form'>
        <h1 className='Title'>PACAF Calculator</h1>
        <form onSubmit={this.handleSubmit}>

          <br />
          <label className='exerciseName'>
            Exercise Name:<p className='required-star'>*</p>
            <input type="text" name="exerciseName" value={this.state.inputs.exerciseName || ''} onChange={this.handleChange} />
          </label>

          <label className='departureCity'>
            From:<p className='required-star'>*</p>
            <input type="text" name="departureCity" value={this.state.inputs.departureCity || ''} onChange={this.handleChange} />
          </label>
          <label className='departureDate'>
            Select a Date:<p className='required-star'>*</p>
            <input type="date" name="departureDate" value={this.state.inputs.departureDate} onChange={this.handleChange} />
          </label>
          <br />
          <label className='arrivalCity'>
            To:<p className='required-star'>*</p>
            <input type="text" name="arrivalCity" value={this.state.inputs.arrivalCity || ''} onChange={this.handleChange} />
          </label>
          <label className='arrivalDate'>
            Select a Date:<p className='required-star'>*</p>
            <input type="date" name="arrivalDate" value={this.state.inputs.arrivalDate} onChange={this.handleChange} />
          </label>
          <br />

          <label className='aircraftType'>
            Aircraft Type:<p className='required-star'>*</p>
            <div className="dropdown">
              <button className="dropdown-toggle" onClick={this.toggleDropdown} type="button">Select Aircraft Type</button>
              <div id="dropdown-content" className="dropdown-content">
                <label>
                  <input
                    type="checkbox"
                    value="F-22"
                    name="aircraftType"
                    onChange={this.handleChange}
                    checked={this.state.inputs.aircraftType && this.state.inputs.aircraftType.includes("F-22")}
                  />
                  F-22
                  {this.state.inputs["F-22"] && <input
                    type="number" name="F-22Amount" onChange={this.handleAmount} />
                  }
                </label>
                <label>
                  <input
                    type="checkbox"
                    value="A-10"
                    name="aircraftType"
                    onChange={this.handleChange}
                    checked={this.state.inputs.aircraftType && this.state.inputs.aircraftType.includes("A-10")}
                  />
                  A-10
                  {this.state.inputs["A-10"] && <input
                    type="number" name="A-10Amount" onChange={this.handleAmount} />
                  }
                </label>
                <label>
                  <input
                    type="checkbox"
                    value="C-5"
                    name="aircraftType"
                    onChange={this.handleChange}
                    checked={this.state.inputs.aircraftType && this.state.inputs.aircraftType.includes("C-5")}
                  />
                  C-5
                  {this.state.inputs["C-5"] && <input
                    type="number" name="C-5Amount" onChange={this.handleAmount} />
                  }
                </label>
                <label>
                  <input
                    type="checkbox"
                    value="C-17"
                    name="aircraftType"
                    onChange={this.handleChange}
                    checked={this.state.inputs.aircraftType && this.state.inputs.aircraftType.includes("C-17")}
                  />
                  C-17
                  {this.state.inputs["C-17"] && <input
                    type="number" name="C-17Amount" onChange={this.handleAmount} />
                  }
                </label>
                <label>
                  <input
                    type="checkbox"
                    value="C-130"
                    name="aircraftType"
                    onChange={this.handleChange}
                    checked={this.state.inputs.aircraftType && this.state.inputs.aircraftType.includes("C-130")}
                  />
                  C-130
                  {this.state.inputs["C-130"] && <input
                    type="number" name="C-130Amount" onChange={this.handleAmount} />
                  }
                </label>
                <label>
                  <input
                    type="checkbox"
                    value="F-15C"
                    name="aircraftType"
                    onChange={this.handleChange}
                    checked={this.state.inputs.aircraftType && this.state.inputs.aircraftType.includes("F-15C")}
                  />
                  F-15C
                  {this.state.inputs["F-15C"] && <input
                    type="number" name="F-15CAmount" onChange={this.handleAmount} />
                  }
                </label>
                <label>
                  <input
                    type="checkbox"
                    value="KC-135"
                    name="aircraftType"
                    onChange={this.handleChange}
                    checked={this.state.inputs.aircraftType && this.state.inputs.aircraftType.includes("KC-135")}
                  />
                  KC-135
                  {this.state.inputs["KC-135"] && <input
                    type="number" name="KC-135Amount" onChange={this.handleAmount} />
                  }
                </label>
              </div>
            </div>
          </label>



          <label className='supporters'>
            Number of Supporters:<p className='required-star'>*</p>
            <input type="number" name="numOfSupporters" value={this.state.inputs.numOfSupporters || ''} onChange={this.handleChange} />
          </label>
          <br />
          <label className='airfare'>
            Airfare Type:<p className='required-star'>*</p>
            <select value={this.state.inputs.flyOption} name="flyOption" onChange={this.handleChange}>
              <option value="">-- Select --</option>
              <option value="militaryAir">Military Air</option>
              <option value="commercialAir">Commercial Air</option>
            </select>
          </label>



          <br />
          <label className='lodging'>
            Lodging:<p className='required-star'>*</p>
            <select value={this.state.inputs.lodging} name="lodging" onChange={this.handleChange}>
              <option value="">-- Select --</option>
              <option value="govLodging">Government Lodging</option>
              <option value="commLodging">Commercial Hotel Lodging</option>
              <option value="fieldConditions">Field Conditions</option>
            </select>
          </label>


          <label>
            Meal Provided:
            <input type="checkbox" checked={this.state.inputs.mealProvided} onChange={this.handleChange} />
          </label>

          {this.state.missingfields && <p className='missingFields'>Please Fill Out All Required Fields</p>}
          <br />
          <button className="calculate" type="submit">Calculate</button>
        </form>
      </div>
    );
  };
}

export default Main;