export const validateFileType = (filename) => {
  const allowed = ['.pdf', '.docx', '.txt', '.csv'];
  const ext = filename.toLowerCase().slice(filename.lastIndexOf('.'));
  return allowed.includes(ext);
};

export const validateFileSize = (file, maxMb = 100) => {
  return file.size <= maxMb * 1024 * 1024;
};

export const validateQuestion = (question) => {
  return question.trim().length > 0 && question.length <= 4096;
};
