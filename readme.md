# ?

- to read 161 page pdf for specific column without any miss reading  
  test: testing for 5 dummy data (pass)  
  test: convert 161 page pdf to txt for column id_pembekal and nama_pembekal (pass) - medium use chatgpt(failed for first QnA), claude ai(failed without QnA because limit), grok(pass for first QnA)  

- to make nama_pembekal (senarai pembekal) search for first word and then second word to find same a (senarai aset spa)  
  test:(cancel)  

- a = nama_pembekal (senarai pembekal)  
- b = id_pembekal (senarai pembekal)  

- c = pembekal (senarai aset spa)  
- d = kod_pembekal (senarai aset spa)  

## requirements

- check 'a' must equal to 'c' (pass)  
- if check is same then take the 'a' value and search for all value that have 'a' in 'c' (pass)  
- if value exist take 'b' value that have 'a' == 'c' (pass)  
- write all 'b' value in 'd' based on all value that exist after search (pass)  

### issue

- some pembekal have two different id_pembekal?  

- 2Y COMMUNICATIONS ENGINEERING | 2Y COMMUNICATIONS ENGINEERING ?

- SKYWORLD CLASSIC (senarai aset spa) | SKY WORLD CLASSIC (senarai pembekal) -> avoid this issue by checking SPACE

- CENTERPOINT SERRVICES SDN BHD (senarai aset spa) | CENTERPOINT SERRVICES SDN BHD (senarai pembekal) -> avoid this issue by checking how much percentage letter same for both without changing the meaning for the full word

- CG COMPUTER SDN BHD (senarai aset spa) | CG COMPUTERS SDN. BHD. (senarai pembekal)-> avoid this issue by checking how much percentage letter same for both without changing the meaning for the full word

- DELCOL WATER SOLUTIONS (M) SDN BHD (senarai aset spa) | DELCOL WATER SOLUTION SDN BHD (senarai pembekal)-> avoid this issue by checking how much percentage letter same for both without changing the meaning for the full word

- DEOMASTER HYGIENE SDN BHD (senarai aset spa) | DEOMASTER HYGIENE SDN. BHD. (senarai pembekal) ->avoid this issue by checking how much percentage letter same for both without changing the meaning for the full word

- DG SOLUTION ENTERPRISE | DG SOLUTION

- DISPLAY ASIA SDN BHD | DISPLAY ASIA SDN. BHD.

- DNA COMPUTER SDN BHD | DNA COMPUTER SERVICE CENTRE

- F H SALES AND SERVICE | F H Sales And Services

- D'URANIUS | DURANIUS ADVERTISING

- FOTO SHANGRI-LA SDN BHD | FOTO SHANGRI-LA (M) SDN.BHD.

- FURNITURE ART | FURNITURE ARTS (M) SDN BHD

- FUTURE MAKERS SDN BHD | FUTUREMAKERS SDN BHD

- GABUNGAN MANTAP SDN BHD | GABUNGAN MANTAP SDN. BHD.

- GEO BILD (M) SDN BHD | GEOBILD (M) SDN BHD

- GLOBAL ELITE VENTURES SDN BHD | GLOBAL ELITE VENTURE SDN BHD

- HERITAGE FORTE SDN. BHD. | HERITAGE FORTE SDN BHD

- High Definition Technology Sdn Bhd | HIGH DEFINITION TECHNOLOGY SDN BHD

- HYDRAMAS (M) SDN BHD | HYDRAMAS M) SDN BHD

- IDAMAN BUMIRIA SDN BHD | IDAMAN BUMIRA SDN BHD

- INFRANET SYSTEM SDN BHD |INFRANET SYSTEMS SDN BHD

- INNATAECH SDN BHD | INNATECH SDN BHD

- INTERNATIONAL CAMERA SERVIS SDN BHD | INTERNATIONAL CAMERA SERVICE SDN BHD

- ITECH JUCTION PTE LTD | ITECH JUNCTION PTE LTD

- JARDINE ONESOLUTION (2001) SDN BHD | JARDINE ONESOLUTION(2001) SDN BHD

- JASAKONTROL AUTOMATION SOLUTION | JASA KONTROL SDN BHD

- JATICOM SND BHD | JATICOM SDN BHD

- JRC-PRO TECHNOLOGY SDN BHD | JRC-PRO TECHNOLOGY S/B

- KAMITERRA | Kamiterra Resources

- KEE HING ELEKTRIK SDN BHD | KEE HING ELEKTRIK SDN BERHAD

- KEJURUTERAAN JAYA TECH SDN. BHD. | KEJURUTERAAN JAYA TECH SDN BHD

- KELISA TECHNOLOGY SDN BHD | KELISA TEKNOLOGY SDN BHD

- KUMPULAN PROTECTION SDN. BHD. | KUMPULAN PROTECTION SDN.BHD.

- MA ASAS JAYA ENTERPRISE | M.A. ASAS JAYA ENTERPRISE

- MEDIA PUTRA COMPUTINDO | CV. MEDIA PUTRA COMPUTINDO

- O TWO JJ SOLUTION | OTWO JJ SOLUTION

- human error? - test upload on git to track changes  

### solution

- fuzzywuzzy

based on this pseudo write for me a python code to make this as simple autoamtion system for proof of concept by using only 5 dummy data. below i provide raw dummy data for senarai pembekal and senarai aset spa (pass by claude ai)  

- senarai pembekal (failed)  

```plaintext
| b       | a                                     |
|---------|---------------------------------------|
| UP02164 | 2Y COMMUNICATIONS ENGINEERING         |
| UP01888 | SKY WORLD CLASSIC                     |
```

- senarai aset spa (failed)  

```plaintext
| d       | c                            |
|---------|------------------------------|
|         |                              |
|         | 2Y COMMUNICATIONS ENGINEERING|
|         | SKYWORLD CLASSIC             |
|         |                              |
|         |                              |
```

- senarai pembekal (pass)

```plaintext
| b       | a                                     |
|---------|---------------------------------------|
| UP02164 | 2Y COMMUNICATIONS ENGINEERING         |
| UP00294 | BROADRAY ELECTRONIC & ELECTRIC TRADIN |
| UP00295 | BRIYANG ENTERPRISE                    |
| UP00296 | BSO TECHNOLOGIES SDN BHD              |
| UP00297 | BSC ELEVATORS SDN BHD                 |
```

- senarai aset spa (pass)  

```plaintext
| d       | c                       |
|---------|-------------------------|
|         |                         |
|         |                         |
|         | BRIYANG ENTERPRISE      |
|         | BSO TECHNOLOGIES SDN BHD|
|         | BSC ELEVATORS SDN BHD   |
```
