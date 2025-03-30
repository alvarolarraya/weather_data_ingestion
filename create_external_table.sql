CREATE OR REPLACE EXTERNAL TABLE `vibrant-shell-455019-h3.weather.daily_weather2`
OPTIONS (
  format = 'JSON',
  uris = ['gs://api_results/*']
);