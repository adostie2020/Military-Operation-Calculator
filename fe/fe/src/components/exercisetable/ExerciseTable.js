import React from 'react';
import axios from 'axios';
import './exercisetable.css'
import PDFGenerator2 from '../jspdf2/createPDF2';


class TheExerciseTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {exercises: []};
        this.handleClick = this.handleClick.bind(this);
    }

    async componentDidMount() {
        await axios.get('https://hackathon-pacaf--thecosmoking.repl.co/api/get_archive')
          .then(response => {
            this.setState({exercises: response.data.archive});
          })
          .catch(error => {
            console.error(error);
          });

          console.log(this.state.exercises);
    }

    handleClick(event){
        PDFGenerator2(event)
    }

    render() {
        return (
            <div>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Location</th>
                                <th>Date Created</th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.exercises.map((exercise) => (
                                <tr key={exercise.id} onClick={() => this.handleClick(exercise)}>
                                    <td>{exercise.exerciseName}</td>
                                    <td>{exercise.toLocation}</td>
                                    <td>{exercise.createdAt}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }

}

export default TheExerciseTable