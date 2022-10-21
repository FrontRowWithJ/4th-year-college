import express from "express";
import fetch from "node-fetch";
import { WeatherData, List, PollutionData, six_tuple, Payload } from "./types";

const PORT = 3000;
const API_KEY = "2e914271572b80555ebd8251540cd5dd";
const AIR_POLLUTION_THRESHOLD = 10;
const HOURS_PER_DAY = 24;
const REGEX = /(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})/i;

const app = express();

app.get("/", async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  const cityName = req.query["cityName"];
  const coords = await getLatLon(cityName as string);
  if (coords === undefined) {
    res.status(404).json({ error: "City Not Found" });
    return;
  }
  const { lat, lon } = coords;
  const uri = `https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`;
  const response = await fetch(uri, { method: "GET" });
  const weatherData = (await response.json()) as WeatherData;
  const { list } = weatherData;
  const days: [List[], List[], List[], List[]] = [[], [], [], []];
  list.forEach((data, i) => days[(i / HOURS_PER_DAY) | 0].push(data));
  const [day1, day2, day3, day4] = days;
  const pollutionURI = `http://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`;
  const pollutionData = (await (
    await fetch(pollutionURI, { method: "GET" })
  ).json()) as PollutionData;
  const airPollution = getAirPollution(pollutionData);
  const payload: Payload = {
    lat,
    lon,
    rainDescription: "",
    weatherDescription: "",
    airPollutionDescription: `The air pollution level is ${airPollution} so you ${
      airPollution >= AIR_POLLUTION_THRESHOLD ? "should" : "dont need to"
    } wear a mask.`,
    day1: getDaysInfo(day1),
    day2: getDaysInfo(day2),
    day3: getDaysInfo(day3),
    day4: getDaysInfo(day4),
  };
  payload.rainDescription = getRainDescription(payload);
  payload.weatherDescription = getWeatherDescription(payload);
  res.json(payload);
});

app.listen(PORT);

const getLatLon: (
  s: string
) => Promise<undefined | { lat: number; lon: number }> = async (
  cityName: string
) => {
  const url = `http://api.openweathermap.org/geo/1.0/direct?q=${cityName}&appid=${API_KEY}&units=metric`;
  const res = await fetch(url, { method: "GET" });
  const body = (await res.json()) as any;
  if (body.length === 0) return undefined;
  const { lat, lon } = body[0];
  return { lat, lon };
};

const getRainData = (hourlyData: List[]) =>
  hourlyData.map(({ rain }) => (rain ? rain["1h"] : 0));

const getTempData = (hourlyData: List[]) =>
  hourlyData.map(({ main }) => main.feels_like.toFixed(2));

const getWindspeedData = (hourlyData: List[]) =>
  hourlyData.map(({ wind: { speed } }) => speed);

const getTodaysAverageTemperature = (hourlyData: List[]) => {
  const avgMin =
    hourlyData.reduce((prev, { main }) => prev + main.temp_min, 0) /
    hourlyData.length;
  const avgMax =
    hourlyData.reduce((prev, { main }) => prev + main.temp_max, 0) /
    hourlyData.length;
  return (avgMax + avgMin) / 2;
};

const getAirPollution = (data: PollutionData) => data.list[0].components.pm2_5;

const getWeekDay = (day: List[]) => {
  const date = day[0].dt_txt;
  const times = REGEX.exec(date)?.slice(1).map(Number) as six_tuple;
  times[1]--;
  return new Date(...times).toLocaleDateString(undefined, { weekday: "long" });
};

const getDaysInfo = (day: List[]) => {
  const rain = getRainData(day);
  const temps = getTempData(day);
  const avgTemp = getTodaysAverageTemperature(day);
  const windSpeeds = getWindspeedData(day);
  const weekday = getWeekDay(day);
  const tempDescription =
    avgTemp <= 12 ? "Cold" : avgTemp <= 24 ? "Mild" : "Hot";
  return { rain, temps, avgTemp, windSpeeds, tempDescription, weekday };
};

const stringify = (input: string[]) => {
  if (input.length === 0) return "";
  if (input.length === 1) return input[0];
  const res = input.slice(0, input.length - 2).join(", ");
  return `${res}${res ? ", " : ""}${input.at(-2)} and ${input.at(-1)}`;
};

const getRainDescription = ({ day1, day2, day3, day4 }: Payload) => {
  const days = [day1, day2, day3, day4];
  const rains = days.map(({ rain }) => rain);
  const weekdays = days.map(({ weekday }) => weekday);
  const rainDays = weekdays.filter((_, i) => rains[i].some((n) => n > 0));
  if (rainDays.length !== 0) {
    return `It's going to rain on ${stringify(
      rainDays
    )} so you should pack an umbrella.`;
  } else return "It's not going to rain so you don't need to pack an umbrella.";
};

const getTempDays = (
  weekdays: string[],
  days: Payload["day1"][],
  tempDescription: "Cold" | "Mild" | "Hot"
) => weekdays.filter((_, i) => days[i].tempDescription === tempDescription);

const getTempDescription = (days: string[], temp: "Cold" | "Mild" | "Hot") =>
  days.length ? `${temp.toLowerCase()} on ${stringify(days)}` : "";

const getWeatherDescription = ({ day1, day2, day3, day4 }: Payload) => {
  const days = [day1, day2, day3, day4];
  const weekdays = days.map(({ weekday }) => weekday);
  const coldDays = getTempDays(weekdays, days, "Cold");
  const mildDays = getTempDays(weekdays, days, "Mild");
  const hotDays = getTempDays(weekdays, days, "Hot");
  const coldDesc = getTempDescription(coldDays, "Cold");
  const mildDesc = getTempDescription(mildDays, "Mild");
  const hotDesc = getTempDescription(hotDays, "Hot");
  const descs = [coldDesc, mildDesc, hotDesc];
  const finalDescs = descs.filter((s) => !!s);
  const packingConditions = ["cold", "mild", "hot"].filter(
    (_, i) => !!descs[i]
  );
  return `It's going to be ${stringify(
    finalDescs
  )} so you should pack for ${stringify(packingConditions)} weather.`;
};
