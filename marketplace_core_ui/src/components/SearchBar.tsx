import { useContext, useEffect, useState } from "react";
import { SearchContext } from "@/context/SearchContext";
import searchicon from '../assets/search.png';
import cross from '../assets/cross.png';
import { useLocation } from "react-router-dom";

const SearchBar = () => {
    const { search, setSearch, showSearch, setShowSearch } = useContext(SearchContext);
    const location = useLocation();
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        if (location.pathname.includes('products')) {
            setVisible(true);
        } else {
            setVisible(false);
        }
    }, [location]);

    if (!showSearch || !visible) {
        return null;
    }

    return (
        <div className="border-t border-b bg-gray-50 text-center">
            <div className="inline-flex items-center justify-center border border-gray-400 px-5 py-2 my-2 mx-3 rounded-full w-3/4 sm:w-1/2">
                <input
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="flex-1 outline-none bg-inherit text-sm"
                    type="text"
                    placeholder="Search"
                />
                <img src={searchicon} alt="search" className="w-4" />
            </div>
            <img
                src={cross}
                alt="cross"
                className="inline w-3 cursor-pointer"
                onClick={() => setShowSearch(false)}
            />
        </div>
    );
};

export default SearchBar;
