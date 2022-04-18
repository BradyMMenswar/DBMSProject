alter table ohlc_data_point add  (low number);

insert into currency values (1,'BTC');
insert into currency values (2,'ETH');
commit;

insert into exchange values (1,'Gemini');
commit;
