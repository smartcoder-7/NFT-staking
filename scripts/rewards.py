import numpy as np
import matplotlib.pyplot as plt

## An mvp python script to model reward payouts

def exponentialDist(tokens : float):
    weights = np.exp(-np.arange(0,10) * 0.7)
    normalization = np.sum(weights)

    return tokens * weights / normalization

totalTokens = 9000
gTokenReserved_month0 = 700
tokensMonth_1_2 = 2000

nG_investors = 240
maxG = 2
minG = 0.1

nP_investors = 50
maxP = 20
minP = 0.5

nM_investors = 10
maxM = 20
minM = 0.0001

tokensAllocationPerMonth = np.zeros(12)
tokensAllocationPerMonth[0:2] = tokensMonth_1_2
tokensAllocationPerMonth[2:] = exponentialDist(totalTokens - np.sum(tokensAllocationPerMonth[0:1]))
plt.plot(tokensAllocationPerMonth, label="Tokens released every month")
plt.legend()
plt.show()

def getReturnWeights(g_net : float, p_net : float, m_net : float):
    order = np.max([np.log(p_net/(g_net + m_net)) / np.log(10), 0])
    d = np.exp(-order)
    normalization = g_net + d * p_net + m_net

    return g_net / normalization,  d * p_net / normalization, m_net / normalization

def invest():
    # fig, ax = plt.subplots(12, 3)

    for month in range(12):
        gReturns = np.zeros(nG_investors)
        pReturns = np.zeros(nP_investors)
        mReturns = np.zeros(nM_investors)

        gInvestment = minG + np.random.rand(nG_investors) * (maxG - minG)
        pInvestment = minP + np.random.rand(nP_investors) * (maxP - minP)
        mInvestment = minM + np.random.rand(nM_investors) * (maxM - minM)

        tokensThisMonth = tokensAllocationPerMonth[month]

        g_net = np.sum(gInvestment)
        p_net = np.sum(pInvestment)
        m_net = np.sum(mInvestment)

        if month == 0:
            tokensThisMonth -= gTokenReserved_month0

            gReturns[:] += gTokenReserved_month0 * gInvestment / g_net

        gW, pW, mW = getReturnWeights(g_net, p_net, m_net)
        print("Weights " + str(month) + " - gW:" + str(gW) + "  pW:" + str(pW)  + "  mW:" + str(mW))

        gReturns[:] += gW * tokensThisMonth * gInvestment / g_net
        pReturns[:] += pW * tokensThisMonth * pInvestment / p_net
        mReturns[:] += mW * tokensThisMonth * mInvestment / m_net

        # ax[month, 0].plot(gReturns, color="r", label="G, Investment:{Investment:.2f}, Return:{Return:.2f}".format(Investment=g_net, Return=np.sum(gReturns)))
        # ax[month, 0].legend(loc="upper right")
        # ax[month, 1].plot(pReturns, color="g", label="P, Investment:{Investment:.2f}, Return:{Return:.2f}".format(Investment=p_net, Return=np.sum(pReturns)))
        # ax[month, 1].legend(loc='upper right')
        # ax[month, 2].plot(mReturns, color="b", label="M, Investment:{Investment:.2f}, Return:{Return:.2f}".format(Investment=m_net, Return=np.sum(mReturns)))
        # ax[month, 2].legend(loc='upper right')


    # plt.show()

invest()
