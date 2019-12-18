module.exports = {
    outputDir: 'dist',
    assetsDir: 'static',
    devServer: {
      // Proxy to Django views for development
      proxy: {
        '/api*': {
          target: 'http://localhost:8000/',
        },
        '/admin*': {
          target: 'http://localhost:8000/'
        },
        // For DRF debugging
        'static/rest_framework': {
          target: 'http://localhost:8000/'
        }
      }
    }
  }