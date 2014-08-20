#!/usr/bin/lua
--Get Content from One.
local http = require "socket.http"
local site = "http://wufazhuce.com"
local site_one = "http://wufazhuce.com/one/vol."
local regex_picture = "<div%sclass=\"one%-imagen\">.-src=\"(.-)\""
local regex_article = "<div%sclass=\"one%-articulo\">(.-)<p%sclass=\"articulo%-editor\">"
local regex_question = "<div%sclass=\"one%-cuestion\">(.-)<div%sclass=\"cuestion%-compartir\">"
local regex_citation = "<div%sclass=\"one%-cita\">(.-)</div>"

local mime = require 'mime'
local ltn12 = require 'ltn12'
local smtp = require 'socket.smtp'

function get_content(str)
	local ret = str:gsub("%sclass=\".-\"", "")
				   :gsub("<p>", "")
				   :gsub("</p>", "<br>")
				   :gsub("<div>", "")
				   :gsub("</div>", "<br>")
	return ret
end

--get vol
local res, state, header = http.request(site)
local vol = arg[1] or string.match(res, "vol%.(%d+)")

--write header
local html_filename = "vol-" .. vol .. ".html"
local f = io.open(html_filename, "w")
f:write("<!DOCTYPE html><html><br>")
f:write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')

--get image
res, state, header = http.request(site_one .. vol)
local img_path = string.match(res, regex_picture)
f:write('<pre><img src="' .. img_path .. '"/></pre><br>')

--get picture txt
local citation_content = string.match(res, regex_citation)
if citation_content then
	local data = get_content(citation_content)
	f:write(data .. "<br>")
end

--get article
local article_content = string.match(res, regex_article)
if article_content then
	local data = get_content(article_content)
	f:write(data .. "<br>")
end

--get question
local question_content = string.match(res, regex_question)
if question_content then
	local data = get_content(question_content)
	f:write(data)
end
f:write("<p>" .. os.date() .. " @leah " .. "</p></html>")
f:close()

local email = function(email_address, path, filename)
	local from 
	if (email_address == nil) or (path == nil) or (filename == nil) then
		return false
	end

	from = "<onenote_leah@163.com>"
	rcpt = {
		"<" .. email_address .. ">"
	}
	mesgt = {
		headers = {
			to = email_address,
			["content-type"] = 'text/html',
			["content-transfer-encoding"] = "BASE64",
			subject = "vol-" .. vol
		},
		body = ltn12.source.chain(
			ltn12.source.file(io.open(path .. filename, "rb")),
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
		password = "lihui0110",
		server = 'smtp.163.com', 
		source = smtp.message(mesgt)
	}
	if e then
		print("\tstatus: failed")
	else
		print("\tstatus: done")
	end

end
print("\tvol: " .. vol)
email("me@onenote.com", "/home/lihui/work/one/daily/", "vol-" .. vol .. ".html")
