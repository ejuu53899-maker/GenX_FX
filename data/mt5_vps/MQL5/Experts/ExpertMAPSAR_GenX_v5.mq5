//+------------------------------------------------------------------+
//|                                     ExpertMAPSAR_GenX_v5.mq5      |
//|               GENX 3.6.9 Smart EA Bridge for Exness MT5 Terminal |
//+------------------------------------------------------------------+
#property copyright "GENX Trading Intelligence System v3.6.9"
#property version   "5.00"

input string   InpBridgeHost = "http://127.0.0.1:8000"; // FastAPI Bridge
input double   InpMaxRiskPct = 1.0;                      // Max Risk %
input string   InpSymbol     = "XAUUSD";                 // Symbol

int OnInit() {
    Print("GENX Exness MT5 EA Bridge initialized in DEMO mode.");
    return(INIT_SUCCEEDED);
}
