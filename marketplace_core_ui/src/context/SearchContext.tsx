import { createContext, useState, ReactNode, useContext } from "react";

interface SearchContextType {
    search: string;
    setSearch: (value: string) => void;
    showSearch: boolean;
    setShowSearch: (value: boolean) => void;
}

const SearchContext = createContext<SearchContextType>({
    search: '',
    setSearch: () => {},
    showSearch: false,
    setShowSearch: () => {},
});

const SearchContextProvider = ({ children }: { children: ReactNode }) => {
    const [search, setSearch] = useState<string>('');
    const [showSearch, setShowSearch] = useState<boolean>(false);

    const value: SearchContextType = {
        search,
        setSearch,
        showSearch,
        setShowSearch,
    };

    return (
        <SearchContext.Provider value={value}>
            {children}
        </SearchContext.Provider>
    );
};


export { SearchContext, SearchContextProvider };
