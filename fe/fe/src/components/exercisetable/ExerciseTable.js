import React from 'react';
import Swal from 'sweetalert2';
import axios from 'axios';


class TheExerciseTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {exercises: []};
    }

    async componentDidMount() {
        await axios.get('https://hackathon-pacaf--thecosmoking.repl.co/api/get_exercise')
          .then(response => {
            this.setState({exercises: response.data.exercises});
          })
          .catch(error => {
            console.error(error);
          });
    }

    swalfirestuff() {
        Swal.fire({
            title: 'Submit new exercise',
            html:
                '<input id="input1" class="swal2-input" placeholder="Enter exercise name">' +
                '<input id="input2" class="swal2-input" placeholder="location">',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Add',
            showLoaderOnConfirm: true,
            preConfirm: () => {
                const newName = document.getElementById('input1').value;
                const newLocation = document.getElementById('input2').value;

                return {newName, newLocation};
            }
        }).then((result) => {
            console.log(result);
            if (result.isConfirmed){
                axios.post('https://hackathon-pacaf--thecosmoking.repl.co/api/add_exercise', {
                    name: result.value.newName,
                    location: result.value.newLocation
                }).then((response) => {
                    console.log("post request success: ", response.data);
                    window.location.reload();
                }).catch((error) => {
                    console.log("error alv: ", error);
                });
            }
        })
    }

    render() {
        return (
            <div>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>Location</th>
                                <th>Name</th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.exercises.map((exercise) => (
                                <tr key={exercise.id}>
                                    <td>{exercise.location}</td>
                                    <td>{exercise.name}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <button onClick={() => this.swalfirestuff()}> enter new exercise</button>
            </div>
        );
    }

}

export default TheExerciseTable