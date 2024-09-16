import { BrowserRouter as Router } from 'react-router-dom';
import AppRouting from './routing/Routing';

const App = () => {
  return (
    <Router>
      <AppRouting />
    </Router>
  );
};

export default App;
