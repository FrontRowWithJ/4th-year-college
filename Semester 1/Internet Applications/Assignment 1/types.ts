export interface WeatherData {
  cod: string;
  message: number;
  cnt: number;
  list: List[];
  city: City;
}

export type List = {
  dt: number;
  main: Main;
  weather: Weather[];
  clouds: Clouds;
  wind: Wind;
  visibility: number;
  pop: number;
  rain?: Rain;
  snow?: Snow;
  sys: Sys;
  dt_txt: string;
};

interface Main {
  temp: number;
  feels_like: number;
  temp_min: number;
  temp_max: number;
  pressure: number;
  sea_level: number;
  grnd_level: number;
  humidity: number;
  temp_kf: number;
}

type Weather = {
  id: number;
  main: string;
  description: string;
  icon: string;
};

type Clouds = {
  all: number;
};

type Wind = {
  speed: number;
  deg: number;
  gust: number;
};

interface Rain {
  "1h": number;
}

interface Snow {
  "1h": number;
}

interface Sys {
  pod: string;
}

interface City {
  id: string;
  name: string;
  coord: { lat: number; lon: number };
  country: string;
  population: number;
  timezone: number;
  sunrise: number;
  sunset: number;
}

export interface PollutionData {
  coord: [number, number];
  list: [
    {
      dt: number;
      main: {
        aqi: number;
      };
      components: {
        co: number;
        no: number;
        no2: number;
        o3: number;
        so2: number;
        pm2_5: number;
        pm10: number;
        nh3: number;
      };
    }
  ];
}

export type six_tuple = [number, number, number, number, number, number];

export interface Payload {
  airPollutionDescription: string;
  rainDescription: string;
  weatherDescription: string;
  lat:number;
  lon:number;
  day1: {
    rain: number[];
    temps: string[];
    avgTemp: number;
    windSpeeds: number[];
    tempDescription: string;
    weekday: string;
  };
  day2: {
    rain: number[];
    temps: string[];
    avgTemp: number;
    windSpeeds: number[];
    tempDescription: string;
    weekday: string;
  };
  day3: {
    rain: number[];
    temps: string[];
    avgTemp: number;
    windSpeeds: number[];
    tempDescription: string;
    weekday: string;
  };
  day4: {
    rain: number[];
    temps: string[];
    avgTemp: number;
    windSpeeds: number[];
    tempDescription: string;
    weekday: string;
  };
}
