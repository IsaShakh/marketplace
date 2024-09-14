const { ModuleFederationPlugin } = require("webpack").container;
const HtmlWebpackPlugin = require("html-webpack-plugin");
const path = require("path");
const deps = require("./package.json").dependencies;

module.exports = {
  entry: "./src/index.tsx",
  mode: "development",
  devServer: {
    static: path.join(__dirname, "dist"),
    port: 3000,
  },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].bundle.js",
    publicPath: "auto",
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
    alias: {
      "@components": path.resolve(__dirname, "src/components/"),
      "@types": path.resolve(__dirname, "src/types/"),
    },
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: "babel-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  plugins: [
    new ModuleFederationPlugin({
      name: "marketplace_ui",
      filename: "remoteEntry.js",
      remotes: {
        host: `promise new Promise(resolve => {
      const hostUrl = 'http://localhost:3001';
      const remoteUrl = hostUrl + '/host.js';
      const script = document.createElement('script');
      script.src = remoteUrl;
      script.onload = () => {
        const proxy = {
          get: (request) => window.host.get(request),
          init: (arg) => {
            try {
              return window.host.init(arg);
            } catch(e) {
              console.error('remote container already initialized');
            }
          }
        }
        resolve(proxy)
      };
      document.head.appendChild(script);
    })`,
      },
      shared: {
        react: {
          singleton: true,
          requiredVersion: deps.react,
        },
        "react-dom": {
          singleton: true,
          requiredVersion: deps["react-dom"],
        },
        "react-router-dom": {
          singleton: true,
          requiredVersion: deps["react-router-dom"],
        },
      },
    }),
    new HtmlWebpackPlugin({
      template: "./public/index.html",
    }),
  ],
};
