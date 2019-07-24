# xAPI_loadingcandles
streaming candles data from xAPI provided

We are connecting to xAPI server, getchartlastrequest method is used for candles retrieval (via websocket).
Once we connected we are calling getchartlastrequest and retrieving candles for last 5 minutes from a server. This is in a indefinetly while loop....In each iteration table is refreshed with last 5 minute candles...


