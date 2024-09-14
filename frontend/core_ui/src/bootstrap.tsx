import ReactDOM from "react-dom/client";
import CustomButton from "./components/Button";
import Layout from "./components/Layout";

const App = () => (
  <Layout>
    <h1>Core UI App</h1>
    <CustomButton />
  </Layout>
);

const rootElement = document.getElementById("root");
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<App />);
}
