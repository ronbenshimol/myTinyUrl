from flask import render_template, redirect, request, jsonify, abort
from app import app
from app.db import getShotUrlByLongUrl, getLongUrlByShortUrl, getLinkEntityByShortUrl, addUrlRequest, getDbStatistics


@app.route('/')
def index():
    return render_template('index.html', title='my url resolver')

@app.route('/stats')
def stats():
    return render_template('statistics.html', title='statistics')


@app.route('/getStatistics')
def getStatistics():
    return jsonify(getDbStatistics())



# return the short url
@app.route('/resolveShortUrl')
def resolveShortUrl():
    longUrl = request.args.get('longUrl')
    shortUrl = {'url': getShotUrlByLongUrl(longUrl)}
    return jsonify(shortUrl)

@app.route('/favicon.ico/')
def favicon(shortUrl):
    abort(404)

# return the long url
@app.route('/<shortUrl>/')
def resolveLongUrl(shortUrl):
    # try to get the long URL by short URL
    LinkEntity = getLinkEntityByShortUrl(shortUrl)
    
    if(LinkEntity != None):
        # update db
        addUrlRequest(LinkEntity[0]) # check this
        redirectUrl = LinkEntity[1]
        return redirect(redirectUrl)
    else:
        # update db
        addUrlRequest(None)
        abort(404)
