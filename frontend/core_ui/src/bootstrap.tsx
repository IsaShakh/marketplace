import ReactDOM from "react-dom/client";
import Layout from "./components/Layout";

const App = () => (
  <Layout>
    <h1>Core UI App</h1>
  </Layout>
);

const rootElement = document.getElementById("root");
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<App />);
}
