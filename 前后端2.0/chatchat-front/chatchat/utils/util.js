const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

const SERVER = 'http://127.0.0.1:8000';

export function request(data, url, method) {
	return new Promise((resolve, reject) => {
		wx.request({
			url: `${SERVER}${url}`,
			data,
			method,
			header: {
				'Content-Type': method == 'GET' ? 'application/json;charset=utf-8' : 'application/x-www-form-urlencoded;',
			},
			success: res => {
				console.log(res.data.state)
				if (res.statusCode == 200 || res.data.state == '成功') {
					return resolve(res.data);
				} else {
					wx.showToast({
						title: res.data.msg,
						icon: "none"
					})
					reject(res.data)
					return
				}
			},
			fail: err => {
				console.log('err')
				reject(err)
			}
		})
	}).catch(err => console.log(err))
}


module.exports = {
  formatTime: formatTime
}
