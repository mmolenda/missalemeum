export const myLocalStorage = {
  getItem: (key: string) => {
    try {
      return localStorage.getItem(key)
    } catch (e) {
      return undefined;
    }
  },
  setItem: (key: string, value: string) => {
    try {
      localStorage.setItem(key, value)
    } catch (e) {
      return undefined;
    }
  },
  removeItem: (key: string) => {
    try {
      localStorage.removeItem(key)
    } catch (e) {
      return undefined;
    }
  }
}