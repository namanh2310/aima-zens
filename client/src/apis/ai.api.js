import axios from "axios";
import { LOCAL_URL } from "../constants/api.const";

export const AIScannerApp = async ({regenerate_status, img}) => {
  const response = await axios.post(
    LOCAL_URL + "ai-scanner/for-app", { regenerate_status, img }
  );
  return response;
}