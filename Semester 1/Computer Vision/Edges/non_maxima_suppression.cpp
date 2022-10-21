// nms_result = gradients.clone();
// for (int row = 1; row < gradients.rows - 1; row++)
//   for (int column = 1; column < gradients.cols - 1; column++)
//   {
//     float curr_gradient = gradients.at<float>(row, column);
//     float curr_orientation = orientations.at<float>(row, column);
//     // Determine which neighbours to check
//     int direction = (((int)(16.0 * (curr_orientation) / (2.0 * PI)) + 15) % 8) / 2;
//     float gradient1 = 0.0, gradient2 = 0.0;
//     switch (direction)
//     {
//     case 0:
//       gradient1 = gradients.at<float>(row - 1, column - 1);
//       gradient2 = gradients.at<float>(row + 1, column + 1);
//       break;
//     case 1:
//       gradient1 = gradients.at<float>(row - 1, column);
//       gradient2 = gradients.at<float>(row + 1, column);
//       break;
//     case 2:
//       gradient1 = gradients.at<float>(row - 1, column + 1);
//       gradient2 = gradients.at<float>(row + 1, column - 1);
//       break;
//     case 3:
//       gradient1 = gradients.at<float>(row, column + 1);
//       gradient2 = gradients.at<float>(row, column - 1);
//       break;
//     }
//     if ((gradient1 > curr_gradient) || (gradient2 > curr_gradient))
//       nms_result.at<float>(row, column) = 0.0;
//   }