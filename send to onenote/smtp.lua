local mime = require 'mime'
local ltn12 = require 'ltn12'
local smtp = require 'socket.smtp'
local email_withattachment = function(email_address, path, filename)
	local from 
	if (email_address == nil) or (path == nil) or (filename == nil) then
		return false
	end

	from = "<onenote_leah@163.com>"
	rcpt = {
		"<"..email_address..">"
	}
	mesgt = {
		headers = {
			to = email_address,
			["content-type"] = 'text/html',
			["content-transfer-encoding"] = "BASE64",
			subject = "subject line"
		},
		body = ltn12.source.chain(
		ltn12.source.file(io.open(path..filename, "rb")),
		ltn12.filter.chain(
		mime.encode("base64"),
		mime.wrap()
		)
		)
	}

	r, e = smtp.send{
		from = from,
		rcpt = rcpt,
		user = "onenote_leah@163.com",
		password = "xxxx",
		server = 'smtp.163.com', 
		source = smtp.message(mesgt)
	}
	print(r, e)
	if e then
		return false
	end
	return true
end
email_withattachment("me@onenote.com", "/home/lihui/work/one/daily/", "vol-577.html")
