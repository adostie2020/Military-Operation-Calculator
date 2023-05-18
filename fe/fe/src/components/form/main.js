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
      formData: [],
      minAmountSupporters: 0,

      exerciseName: "",

      fromLocation: "",
      startDate: "",

      toLocation: "",
      endDate: "",

      peopleCommercialAir: 0,
      peopleMilitaryAir: 0,

      peopleGovernmentLodging: 0,
      peopleCommercialLodging: 0,
      peopleWoodsLodging: 0,

      peoplePerDiemRate: 0,
      peoplePerDiemFood: 0
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleAmount = this.handleAmount.bind(this);
    this.onComplete = this.onComplete.bind(this);
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

  onComplete(event) {
    event.preventDefault();
    console.log(this.state.inputs);
    console.log(this.state.formData);
    console.log(this.state.minAmountSupporters);

    console.log(this.state.peopleCommercialAir);
    console.log(this.state.peopleMilitaryAir);

    console.log(this.state.peopleCommercialLodging);
    console.log(this.state.peopleGovernmentLodging);
    console.log(this.state.peopleWoodsLodging);

    console.log(this.state.peoplePerDiemRate);
    console.log(this.state.peoplePerDiemFood);

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

    const aircraftName = name.substring(0, name.length - 6);
    this.state.aircrafts.map((aircraft, i) => {
      if (aircraft.type === aircraftName) {
        this.setState({ minAmountSupporters: this.state.minAmountSupporters + aircraft.personnel[value - 1] });
      }
    })
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
      if (this.state.inputs["A-10"] || this.state.inputs["C-5"] || this.state.inputs["C-17"] || this.state.inputs["C-130"] || this.state.inputs["F-15C"] || this.state.inputs["F-22"] || this.state.inputs["KC-135"]) {
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

  handleInputAmount = (event) => {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  };

  async toggleDropdown() {
    var dropdownContent = document.getElementById("dropdown-content");
    dropdownContent.style.display = dropdownContent.style.display === "none" ? "block" : "none";
  }

  render() {
    return (
      <div className='Form'>
        <h1 className='Title'>PACAF Calculator</h1>
        <form onSubmit={this.onComplete}>

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
            <input type="number" name="numOfSupporters" value={this.state.minAmountSupporters} onChange={this.handleChange} />
          </label>

          <label className='airfare'>

            <br/>
            Amount in Military Air:<p className='required-star'>*</p>
            <input type="number" name="peopleMilitaryAir" value={this.state.peopleMilitaryAir} onChange={this.handleInputAmount}/>

            Amount in Commercial Air:<p className='required-star'>*</p>
            <input type="number" name="peopleCommercialAir" value={this.state.peopleCommercialAir} onChange={this.handleInputAmount}/>
          </label>




          <label className='lodging'>

            <br/>
            Amount in government lodging:<p className='required-star'>*</p>
            <input type="number" name="peopleGovernmentLodging" value={this.state.peopleGovernmentLodging} onChange={this.handleInputAmount}/>

            Amount in commercial hotel lodging:<p className='required-star'>*</p>
            <input type="number" name="peopleCommercialLodging" value={this.state.peopleCommercialLodging} onChange={this.handleInputAmount}/>

            Amount in field conditions:<p className='required-star'>*</p>
            <input type="number" name="peopleWoodsLodging" value={this.state.peopleWoodsLodging} onChange={this.handleInputAmount}/>
          </label>


          <label>
            
            <br/>
            Amount in per diem rate:<p className='required-star'>*</p>
            <input type="number" name="peoplePerDiemRate" value={this.state.peoplePerDiemRate} onChange={this.handleInputAmount}/>

            Amount in per diem food:<p className='required-star'>*</p>
            <input type="number" name="peoplePerDiemFood" value={this.state.peoplePerDiemFood} onChange={this.handleInputAmount}/>
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