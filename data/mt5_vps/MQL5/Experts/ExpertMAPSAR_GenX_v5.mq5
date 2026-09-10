//+------------------------------------------------------------------+
//|                                     ExpertMAPSAR_GenX_v5.mq5      |
//|               GENX 3.6.9 Smart EA Bridge for Exness MT5 Terminal |
//+------------------------------------------------------------------+
#property copyright "GENX Trading Intelligence System v3.6.9"
#property link      "https://gitlab.com/genxdbxfx3/warp.git"
#property version   "5.00"

#include <Trade\Trade.mqh>

input string   InpBridgeHost = "http://127.0.0.1:8000"; // FastAPI Bridge Host
input double   InpMaxRiskPct = 1.0;                      // Max Risk %
input string   InpSymbol     = "XAUUSD";                 // Default Symbol

int OnInit()
  {
   Print("GENX v3.6.9 EA Bridge initialized for Exness MT5 VPS.");
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   Print("GENX v3.6.9 EA Bridge deinitialized.");
  }

void OnTick()
  {
   // EA Tick Handler communicates signal requests with FastAPI Bridge
  }
