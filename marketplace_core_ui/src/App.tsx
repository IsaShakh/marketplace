import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import SearchBar from './components/SearchBar';
import Home from './pages/Home';
import Products from './pages/Products';
import Product from './pages/Product';
import { SearchContextProvider } from "./context/SearchContext";


const App = () => {
  return (
    <SearchContextProvider>
      <div className="px-4 sm:px-[5vw] md:px-[7vw] lg:px-[9vw]">
        <Navbar />
        <SearchBar />
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/products' element={<Products />} />
          <Route path='/product/:productId' element={<Product />} />
        </Routes>
      </div>
    </SearchContextProvider>
  );
}

export default App;
