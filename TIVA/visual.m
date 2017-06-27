
function Image=visual(qmf, L, j, n_1, n_2)
W_1 = zeros(256, 256);
W_2 = zeros(256, 256);
W_3 = zeros(256, 256);
a = 2^(8-j);
W_1(n_1, a+n_2) = 1;
W_2(a+n_1, n_2) = 1;
W_3(a+n_1, a+n_2) = 1;
I_1 = IWT2_PO(W_1, L, qmf);
I_2 = IWT2_PO(W_2, L, qmf);
I_3 = IWT2_PO(W_3, L, qmf);
for i=1:256
	for j=1:256
		if I_3(i, j)==0
			I_3(i, j) = 0.0001;
		end
	end
end
Image = (I_1.*I_2)./I_3;
disp(size(Image));
figure(2)
surf(Image);
colormap('copper');
shading interp;
end
