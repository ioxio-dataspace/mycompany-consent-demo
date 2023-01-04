/** @jsx jsx */
import { jsx, Spinner } from "theme-ui"
import { useState, useEffect } from "react"
import {
  Container,
  DataProduct,
  Text,
  ShareModal,
  OwnershipDataTable,
  Button,
} from "components"
import { API, ConsentTokenManager } from "utilities"

import prhLogo from "assets/images/prh-logo.png"
import myBisLogo from "assets/images/mybis-dark-logo.svg"

const STANDARD = "draft/Company/Shareholders"
const DATA_SOURCE = "ioxio:v2"

const DATA_PRODUCTS = [
  {
    name: "Beneficial owners",
    description: "Finnish Patent and Registration Office",
    image: prhLogo,
  },
  {
    name: "List of shareholders",
    description: "mybis register",
    isForSharing: true,
    image: myBisLogo,
  },
]

function OwnershipView({ company = {}, configuration = {} }) {
  const [ownershipData, setOwnershipData] = useState({
    owners: [],
    shareSeries: [],
    isLoading: true,
    error: "",
  })

  const [dataProductToShare, setDataProductToShare] = useState({})
  const [verifyConsentUrl, setVerifyConsentUrl] = useState()
  const [isConsentRequired, setIsConsentRequired] = useState()

  const openModal = (dataProduct) => {
    setDataProductToShare(dataProduct)
  }

  const onModalCloseClick = () => {
    setDataProductToShare({})
  }

  const requestConsent = async () => {
    ConsentTokenManager.removeToken(
      STANDARD,
      DATA_SOURCE,
      configuration.nexusBaseDomain
    )
    const dppUri = ConsentTokenManager.makeDppUri(
      STANDARD,
      DATA_SOURCE,
      configuration.nexusBaseDomain
    )
    const resp = await API.requestConsent(dppUri)

    // need to redirect user to verification page of Consent provider
    if (resp.ok && resp.data.type === "verifyUserConsent") {
      const currentUrl = window.location.href.split("?")[0]
      setVerifyConsentUrl(`${resp.data.verifyUrl}?returnUrl=${currentUrl}`)
    }

    // consent is granted, save consent token
    else if (resp.ok && resp.data.type === "consentGranted") {
      ConsentTokenManager.setToken(
        STANDARD,
        DATA_SOURCE,
        configuration.nexusBaseDomain,
        resp.data.consentToken
      )
      // next line will cause useEffect to be triggered again, and
      // to request data source one more time. but this time, with a consent token
      setIsConsentRequired(false)
    }
  }

  const checkDataSourceRequiresConsent = ({ ok, status, error }) => {
    return !ok && status === 502 && error.status === 403
  }

  useEffect(() => {
    ;(async () => {
      if (company.hasOwnProperty("businessId")) {
        const { ok, status, data, error } = await API.getOwnershipData(
          company.businessId,
          configuration.nexusBaseDomain
        )
        if (checkDataSourceRequiresConsent({ ok, status, error })) {
          await requestConsent()
        }

        if (ok) {
          setOwnershipData({
            owners: data.owners,
            shareSeries: data.shareSeries,
            error: "",
            isLoading: false,
          })
        } else {
          setOwnershipData({ owners: [], shareSeries: [], error, isLoading: false })
        }
      }
    })()
  }, [company, isConsentRequired])

  const onRequestConsentClick = () => {
    window.location.href = verifyConsentUrl
  }

  ownershipData.owners.forEach((o) => {
    o.totalShares = 0
    o.totalVotes = 0
    o.ownerships.forEach((os) => {
      o.totalShares += os.quantity

      const series = ownershipData.shareSeries.find(
        (ss) => ss.seriesName === os.seriesName
      )

      if (typeof series !== "undefined") {
        o.totalVotes += os.quantity * series.votesPerShare
      }
    })
  })

  ownershipData.totalSharesAllSeries = 0
  ownershipData.totalVotesAllSeries = 0

  ownershipData.shareSeries.forEach((s) => {
    ownershipData.totalSharesAllSeries += s.totalShares
    ownershipData.totalVotesAllSeries += s.totalShares * s.votesPerShare
  })

  return (
    <Container
      csx={{
        variant: ["flex.column", "flex.column", "flex.row"],
        flexWrap: "wrap",
        justifyContent: [null, null, "space-between"],
      }}
    >
      <Container
        csx={{
          variant: "flex.columnCenterNoMargin",
          mb: [5],
          justifyContent: "start",
          flex: "40%",
        }}
      >
        {ownershipData.isLoading && <Spinner sx={{ m: 3 }} />}
        {verifyConsentUrl && (
          <Container csx={{ variant: "flex.columnCenter" }}>
            <Text>Data source requires a consent to view this data</Text>
            <Button csx={{ mt: 2 }} onClick={onRequestConsentClick}>
              Request consent
            </Button>
          </Container>
        )}
        {!ownershipData.isLoading && (
          <OwnershipDataTable ownershipData={ownershipData} />
        )}
      </Container>

      <Container
        csx={{
          variant: "flex.columnCenterNoMargin",
          justifyContent: "start",
          alignItems: "start",
          mt: [5, 5, 0],
          flex: "0 0 23rem",
        }}
      >
        <Text csx={{ variant: "text.sectionHeader" }}>DATA</Text>

        <Container csx={{ mt: [3] }}>
          {DATA_PRODUCTS.map((d) => {
            return (
              <DataProduct
                baseProps={{
                  onClick: d.isForSharing ? openModal.bind(this, d) : () => false,
                }}
                key={d.name}
                csx={{ my: 3 }}
                isForSharing={d.isForSharing}
                image={d.image}
                name={d.name}
                description={d.description}
              />
            )
          })}
        </Container>
      </Container>

      <ShareModal
        shareOptions={configuration.shareOptions}
        shareFrom={company.id}
        dataProduct={dataProductToShare}
        isOpen={dataProductToShare.hasOwnProperty("name")}
        onCloseClick={onModalCloseClick}
      />
    </Container>
  )
}

export default OwnershipView
