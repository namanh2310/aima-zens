import axios from "axios";
import { LOCAL_URL } from "../constants/api.const";

export const AIScannerApp = async (img) => {
  const response = await axios.post(
    LOCAL_URL + "ai-scanner/for-app", { img }
  );
  return response;
}