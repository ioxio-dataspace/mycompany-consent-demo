class ConsentTokenManager {
  localKey = 'consentToken'

  getToken(standard, source, nexusBaseDomain) {
    const uri = this.makeDppUri(standard, source, nexusBaseDomain)
    return localStorage.getItem(`${this.localKey}-${uri}`) || ''
  }

  setToken(standard, source, nexusBaseDomain, token) {
    const uri = this.makeDppUri(standard, source, nexusBaseDomain)
    localStorage.setItem(`${this.localKey}-${uri}`, token)
  }

  removeToken(standard, source, nexusBaseDomain) {
    const uri = this.makeDppUri(standard, source, nexusBaseDomain)
    localStorage.removeItem(`${this.localKey}-${uri}`)
  }

  makeDppUri(standard, source, nexusBaseDomain) {
    return `dpp://${source}@${nexusBaseDomain}/${standard}`
  }
}

const instance = new ConsentTokenManager()

export default instance
