const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  mode: 'development', // Can be 'production' for optimized builds
    entry: './src/main.js', // Your main JavaScript file
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'), // Output directory
    clean: true, // Clean the output directory before each build
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'], // For CSS files
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './index.html', // Path to your existing index.html
      filename: 'index.html', // Output HTML file name
    }),
  ],
  devServer: {
    static: './dist', // Serve content from the 'dist' directory
    open: true, // Open the browser after server starts
  },
};
