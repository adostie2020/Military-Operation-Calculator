import logo from './logo.svg';
import './App.css';
import HomePage from './components/home/HomePage';
import AircraftTable from './components/home/AircraftTable-Page';
import ExerciseTable from './components/home/ExerciseTable-page';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<HomePage />}></Route>
        <Route path='/aircraftTable' element={<AircraftTable />}></Route>
        <Route path='/exerciseTable' element={<ExerciseTable />}></Route>
      </Routes>
    </Router>
  );
}

export default App;