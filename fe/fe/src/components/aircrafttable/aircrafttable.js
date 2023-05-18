import React from 'react';
import Swal from 'sweetalert2';
import axios from 'axios'
import './aircrafttable.css'

class TheAircraftTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {aircrafts: []};
    }

    async componentDidMount() {
        await axios.get('https://hackathon-pacaf--thecosmoking.repl.co/api/get_aircraft')
          .then(response => {
            this.setState({aircrafts: response.data.aircrafts});
          })
          .catch(error => {
            console.error(error);
          });
    }

    render() {
        return (
            <div>
                <div>
                    <table>
                        <thead>
                        <tr>
                            <th>type</th>
                            <th>amount</th>
                            <th>personnel</th>
                        </tr>
                        </thead>
                        <tbody>
                            {this.state.aircrafts.map((perro, i) => {
                                return perro.personnel.map((personel, j) => {
                                    return (<tr>
                                        <td>{j == 0 ? perro.type : ' '}</td>
                                        <td>{j + 1}</td>
                                        <td>{personel != 0 ? personel : 'n/a'}</td>
                                    </tr>);
                                });
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}

export default TheAircraftTable;