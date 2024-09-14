import ReactDOM from "react-dom/client";

import MarketplaceComponent from "@components/MarketplaceComponent";

const App = () => {
  return <MarketplaceComponent />;
};

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(<App />);
