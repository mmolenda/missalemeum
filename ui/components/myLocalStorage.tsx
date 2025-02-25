export const myLocalStorage = {
  getItem: (key) => {
    try {
      return localStorage.getItem(key)
    } catch (e) {
      return undefined;
    }
  },
  setItem: (key, value) => {
    try {
      localStorage.setItem(key, value)
    } catch (e) {
      return undefined;
    }
  },
  removeItem: (key) => {
    try {
      localStorage.removeItem(key)
    } catch (e) {
      return undefined;
    }
  }
}