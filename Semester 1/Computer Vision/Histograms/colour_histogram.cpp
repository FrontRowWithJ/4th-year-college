// MatND *histogram = new MatND[image.channels()];
// vector<Mat> channels(image.channels());
// split(image, channels);
// const int *channel_numbers = {0};
// float channel_range[] = {0.0, 255.0};
// const float *channel_ranges = channel_range;
// int number_bins = 64;
// for (int chan = 0; chan < image.channels(); chan++)
//   calcHist(&(channels[chan]), 1, channel_numbers, Mat(),
//            histogram[chan], 1, &number_bins, &channel_ranges);