import { CircularProgress } from "@mui/material";

const LoadingOverlay = () => (
  <div class="loading-overlay">
    <div class="loading-spinner">
      <CircularProgress />
    </div>
  </div>
);

export default LoadingOverlay;
