const { ModuleFederationPlugin } = require("webpack").container;
const HtmlWebpackPlugin = require("html-webpack-plugin");
const path = require("path");
const deps = require("./package.json").dependencies;

module.exports = {
  entry: "./src/index.tsx",
  mode: "development",
  devServer: {
    static: path.join(__dirname, "build"),
    port: 3001,
  },
  output: {
    publicPath: "auto",
    filename: "[name].js",
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
      name: "host",
      filename: "host.js",
      exposes: {
        "./Button": "./src/components/Button",
        "./Layout": "./src/components/Layout",
      },
      shared: [
        {
          react: {
            singleton: true,
            requiredVersion: deps["react"],
          },
        },
        {
          "react-dom": {
            singleton: true,
            requiredVersion: deps["react-dom"],
          },
        },
        {
          "react-router-dom": {
            singleton: true,
            requiredVersion: deps["react-router-dom"],
          },
        },
        {
          antd: {
            singleton: true,
            requiredVersion: deps["antd"],
          },
        },
      ],
    }),
    new HtmlWebpackPlugin({
      template: "./public/index.html",
    }),
  ],
};
