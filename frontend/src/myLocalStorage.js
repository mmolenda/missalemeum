export const myLocalStorage = {
	getItem: (key) => {
    try {
			localStorage.getItem(key)
    } catch(e) {
			return undefined;
    }
	},
	setItem: (key, value) => {
    try {
			localStorage.setItem(key, value)
    } catch(e) {
			return undefined;
    }
	}
}