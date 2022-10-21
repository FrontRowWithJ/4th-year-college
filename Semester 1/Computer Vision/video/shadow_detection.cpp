// Ptr<BackgroundSubtractorMOG2> gmm =
//     createBackgroundSubtractorMOG2();
// gmm->apply(current_frame, foreground_mask);
// gmm(current_frame, foreground_mask);
// threshold(foreground_mask, moving_points, 150, 255, THRESH_BINARY);
// ... threshold(foreground_mask, changing_points, 50, 255, THRESH_BINARY);
// absdiff(moving_points, changing_points, shadow_points);
// ... Mat mean_background_image;
// gmm->getBackgroundImage(mean_background_image);