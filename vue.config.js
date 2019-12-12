module.exports = {
    outputDir: 'dist',
    assetsDir: 'static',
    // baseUrl: IS_PRODUCTION
    // ? 'http://cdn123.com'
    // : '/',
    // For Production, replace set baseUrl to CDN
    // And set the CDN origin to `yourdomain.com/static`
    // Whitenoise will serve once to CDN which will then cache
    // and distribute
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