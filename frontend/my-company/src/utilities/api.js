import { getPublicUrl, ConsentTokenManager } from 'utilities'

class API {
  baseUrl = ''
  defaultErrorMessage = 'Oops, something went wrong.'

  constructor() {
    this.baseUrl = '/api'
    this.returnUrl = '/company-select'
  }

  async responseWrapper(r) {
    try {
      if (r.ok) {
        return { ok: r.ok, data: await r.json(), status: r.status }
      } else {
        const json = await r.json()
        const error = json.detail ? json.detail : json
        return {
          ok: r.ok,
          error: error || r.text(),
          status: r.status,
        }
      }
    } catch (e) {
      return { ok: false, error: this.defaultErrorMessage }
    }
  }

  async health() {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    )
  }

  async getIdentity(id) {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/identities/${id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    )
  }

  async updateConsent(from, to, data) {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/consents/from/${from}/to/${to}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data,
        }),
      })
    )
  }

  async readConsent(from, to) {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/consents/from/${from}/to/${to}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    )
  }

  async requestConsent(dataSource) {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/consents/request`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          dataSource,
        }),
      })
    )
  }

  async getCompanyBasicInfo(companyId, source = 'digitalliving') {
    return this.responseWrapper(
      await fetch(
        `${this.baseUrl}/dataProduct/draft/Company/BasicInfo?source=${source}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            companyId,
          }),
        }
      )
    )
  }

  async getOwnershipData(companyId, nexusBaseDomain, source = 'digitalliving:v2') {
    return this.responseWrapper(
      await fetch(
        `${this.baseUrl}/dataProduct/draft/Company/Shareholders?source=${source}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Consent-Token': ConsentTokenManager.getToken(
              'draft/Company/Shareholders',
              source,
              nexusBaseDomain
            ),
          },
          body: JSON.stringify({
            companyId,
          }),
        }
      )
    )
  }

  async startLogin() {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/auth/start_login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          returnPath: `${getPublicUrl()}${this.returnUrl}`,
          frontendPath: getPublicUrl(),
        }),
      })
    )
  }

  async logout() {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    )
  }

  async getUserData() {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/auth/me`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    )
  }

  async getConfiguration() {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/configuration`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    )
  }

  async listLinks(id, direction) {
    return this.responseWrapper(
      await fetch(`${this.baseUrl}/identities/${id}/links/${direction}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    )
  }
}

const instance = new API()

export default instance
