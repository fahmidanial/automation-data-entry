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
- human error? - test upload on git to track changes  

based on this pseudo write for me a python code to make this as simple autoamtion system for proof of concept by using only 5 dummy data. below i provide raw dummy data for senarai pembekal and senarai aset spa (pass by claude ai)  

- senarai pembekal (pass)  

```
| b       | a                                     |
|---------|---------------------------------------|
| UP00293 | BRILLIANT ENTERPRISE                  |
| UP00294 | BROADRAY ELECTRONIC & ELECTRIC TRADIN |
| UP00295 | BRIYANG ENTERPRISE                    |
| UP00296 | BSO TECHNOLOGIES SDN BHD              |
| UP00297 | BSC ELEVATORS SDN BHD                 |
```

- senarai aset spa (pass)  

```
| d       | c                       |
|---------|-------------------------|
|         |                         |
|         |                         |
|         | BRIYANG ENTERPRISE      |
|         | BSO TECHNOLOGIES SDN BHD|
|         | BSC ELEVATORS SDN BHD   |
```
